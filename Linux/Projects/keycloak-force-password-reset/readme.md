# Keycloak force password reset

Bulk-triggers Keycloak's "Update Password" required action for a list of usernames in a realm, sending each user an email with a link to set a new password. Useful after a security incident or before decommissioning shared/default passwords.

## Prerequisites

`kcadm.sh` must be authenticated before running the script:

```bash
/opt/keycloak/bin/kcadm.sh config credentials \
  --server http://localhost:8080 \
  --realm master \
  --user <admin-username> \
  --password '<admin-password>'
```

## Usage

Edit the `USERNAMES` array and `REALM`/`LIFESPAN` variables in `force-password-reset.sh` as needed, then run:

```bash
./force-password-reset.sh
```

`LIFESPAN` is the validity of the reset link in seconds (default 259200 = 72 hours).

## Notes

- `-n` (no-merge) is required on the `update` call, otherwise `kcadm` performs an internal GET on this action endpoint (which doesn't support GET) and the command fails with "Resource not found".
- `lifespan` must be passed as a query parameter in the URL, not via `-s`, because the request body for this endpoint is a JSON array, not an object.
