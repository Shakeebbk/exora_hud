kill -10 $(ps -ef | grep video_exora.py | awk '{print $2}')
