# berlin-residence-permit-appointment
Python script for trying to get an appointment slot for the residence permit in Berlin. The `helplessly-try.sh` will repeatedly run the Python script until the appointment don't return any error. After this point, it is necessary to finish the appointment manually (only because I never saw the following pages to finish the bot).

## Requirements
```bash
$ brew install chromedriver
$ python3 -m pip install selenium
$ python3 -m pip install seleniumwire
```

## Run it
After installing the dependencies above, run:
```bash
./helplessly-try.sh
```
