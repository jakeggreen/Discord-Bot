from datetime import datetime, timezone

def localizeTimezoneStr(dt_obj, target_tz, dt_format) -> str:
	#if dt is Naive make it Aware (assumes correct conversion is to UTC)
	if dt_obj.tzinfo is None:
		dt_obj = dt_obj.replace(tzinfo = timezone.utc)
		#print("set to tz info to utc")
	return dt_obj.astimezone(target_tz).strftime(dt_format)


def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		print(timer, end="\r")
		time.sleep(1)
		t -= 1