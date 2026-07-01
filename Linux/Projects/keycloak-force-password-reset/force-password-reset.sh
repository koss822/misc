#!/bin/bash
set -uo pipefail

REALM="master"
KCADM="/opt/keycloak/bin/kcadm.sh"
LIFESPAN=259200   # 72 hours in seconds, adjust as needed

USERNAMES=(
  user1
  user2
  user3
)

OK=0
FAIL=0
SKIPPED=0

for username in "${USERNAMES[@]}"; do
  echo "=== $username ==="
  USER_ID=$($KCADM get users -r "$REALM" -q username="$username" --fields id --format csv --noquotes 2>/dev/null | tail -n1)

  if [ -z "$USER_ID" ]; then
    echo "  ⚠️  user not found, skipped"
    SKIPPED=$((SKIPPED+1))
    continue
  fi

  # -n (no-merge) is required, otherwise kcadm does an internal GET on this
  # action endpoint, which doesn't support it, and the whole command fails
  # with "Resource not found".
  # lifespan is passed as a query parameter in the URL for this endpoint, not
  # via -s (the body is a JSON array, not an object, so -s can't be used on it).
  if $KCADM update "users/$USER_ID/execute-actions-email?lifespan=${LIFESPAN}" -r "$REALM" -n \
      -b '["UPDATE_PASSWORD"]'; then
    echo "  ✅ email sent (user_id=$USER_ID)"
    OK=$((OK+1))
  else
    echo "  ❌ ERROR sending email (user_id=$USER_ID)"
    FAIL=$((FAIL+1))
  fi
done

echo ""
echo "=== Summary ==="
echo "Sent:    $OK"
echo "Failed:  $FAIL"
echo "Skipped: $SKIPPED"
