# Reporter Manual

## Description

**Reporter** is program counting Q1 result times from log files of the
Formula 1 - Monaco 2018 Racing

## Using html web-interface

Use the address bar of your browser.

### Show the common statistic of the race

> **http://127.0.0.1:5000/report/**

### Show the common statistic of the race in descendig order

> **http://127.0.0.1:5000/report/?order=desk**

### Show the cdrivers names and codes of them

> **http://127.0.0.1:5000/report/drivers/**

### Show the driver statistic

For this click the abbriviatin link on page, or manually enter the abbreviation
in the address bar, for example:

> **http://127.0.0.1:5000/report/drivers/?driver_id=SVF**

## Using comand line interface (CLI)

Reporter uses comand line interface (CLI)

### Show list of drivers and optional order (default order is asc)

> **python report.py --files <folder_path> [--asc | --desc]**

If some dirrectories names contains spaces then use '' .
For example:

> **report.py --files /home/user/Desktop/'Log files'/**

### Show statistic about driver 

> **python report.py --files <folder_path> --driver 'Sebastian Vettel'**

Please, take your attention: if your string contain spaces - insert your text
between ' ' characters.