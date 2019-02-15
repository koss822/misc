## [S3Logs](https://github.com/koss822/misc/tree/master/Aws/s3logs)

This tools watches logs directory where are the S3 Logs files stored with Lambda script located in _aws_ directory and when there is triggered S3 bucket event - _ObjectCreated_ on directory where S3 logs are stored the lambda script creates the message in SQS (Simple Queue Service) and delete log file.

After that there is running SystemD daemon on Linux machine with MySQL installed called s3logs_daemon.py (stored in _scripts_ directory) which check SQS queue for new logs and insert them into MySQL database.

Please be informed that there is no frontend - the main reason is that I find using PHPMyAdmin more universal and better because I can create directly SQL queries which I like.

### Diagram
![S3 Logs diagram](https://raw.githubusercontent.com/koss822/misc/master/imgs/s3logssmall.jpg "S3 Logs diagram")

[large image](https://raw.githubusercontent.com/koss822/misc/master/imgs/s3logslarge.jpg)

### Installation

_some image tutorial is stored in_ [imgs directory](https://github.com/koss822/misc/tree/master/Aws/s3logs/imgs)

1. Clone repository to your directory
2. Set-up S3 logs in directory you like
3. Create lambda function (source file is stored in _aws_ directory) which is triggered by CloudWatch event _ObjectCreated_ on S3 Logs directory.
4. Set-up SQS queue
5. Wait few hours (S3 logs are created only every few hours not on every access)
6. Check SQS queue that it contains messages
7. Install MySQL, PhpMyAdmin, Apache
8. Create database with initial structure (sql file is in the _scripts_ directory)
9. Install scripts and SystemD service files
10. Start and enable SystemD service

Of course do not forget to change variables in various script files. Also the path where scripts should be installed is visible in the source files.
