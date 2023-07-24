# VKtask
A small program for getting your friends from VK

## Authorization
To use it, you need to provide your authorization token and user id. The easiest way to do this is to run the program with --authorize to get the link. Open it in your browser of choice (if it shows "don't copy blah blah blah..." right away, try opening it in incognito mode). Sign in and authorize the app. You will be redirected to a new link. You can get your token from "access_token" parameter of the link and your user id from "user_id"

To ease the use of this program, put your token and user id into the "settings.cfg" file like this:
```
token=vk1.a.asdfasdf123
user=123456
```

## Usage
This program is meant to output your friend list in one of the following formats: CSV, TSV, JSON. You can specify which format you want (CSV by default) and the path to the output file ("report" by default) using the command line arguments (see Interface below). 

If you set up "settings.cfg" as mentioned in Authorization, you can run this program without supplying the --user and --token arguments.

## Interface
```
usage: vkfriends.py [-h] [--format {CSV,TSV,JSON}] [--path PATH] [--token TOKEN] [--user USER] [--authorize]
options:
  -h, --help            show help message
  --format {CSV,TSV,JSON}, -f {CSV,TSV,JSON}
                        output file format
  --path PATH, -p PATH  output file path
  --token TOKEN, -t TOKEN
                        authorization token
  --user USER, -u USER  id of the user to grab friends from
  --authorize           show OAuth link for authorization and exit
```
