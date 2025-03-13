# Loki

## Parsing user agents
<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/loki1.png" alt="loki" />

<img src="https://raw.githubusercontent.com/koss822/misc/master/imgs/loki2.png" alt="loki" />

**Pattern**
```
<ip> - <username> [<timestamp>] "<method> <url> HTTP/<http_version>" <status> <size> "<referrer>" "<user_agent>"
```

**Raw query**
```
count by(user_agent) (count_over_time({app="mediawiki"} | pattern `<ip> - <username> [<timestamp>] "<method> <url> HTTP/<http_version>" <status> <size> "<referrer>" "<user_agent>"` [1h]))
```