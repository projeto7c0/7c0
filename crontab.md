* * * * * nohup python3 7c0-capturas/update_from_list.py > logs/capture.log 2> err_logs/capture_err.log &
0 * * * * nohup python3 7c0-capturas/update_tweets.py 20000 > logs/capture.log 2> err_logs/capture_err.log &
