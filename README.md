## Mubla
### photo album

None of us should be storing our photos and videos in the cloud. Or atleast we should avoid it as much as possible.

Personally, I have my files stored on an SSD(with multiple backups) so that I can access the files on any device within my home using this repository.

Originally we were using some third party apps to browse our photo/video library, but I didn't fully trust what those apps may have been accessing.

So I made Mubla.

### Setup

** This has been made using Linux, so you may need to add some extra code to run it on Windows or Mac **

My directory is set up like this;

photos/year/month/day/<filename>

- year
  - month
    - day
      - file

so, for example;

- photos(root)
  - 2020(year)
    - 01(month)
      - 05(day)
        - video 1(file)
        - video 2
      - 17(day)
        - photo 1
        - photo 2
    - 02(month)
      - 13
        - photo1
        - photo2
        - video 1
      - 25
        - photo1
        - photo2
        - photo3
        - photo4
      - 29
        - photo1
        - photo2
        - video 1

I would recommend you organize your photos/videos in the same manner to use this flask app without problems.

- clone this repository
- change the path in the main.py file to your photos path
- setup the virtual environment
- use the command > flask run --host=0.0.0.0 (withrout the host argument it will only be available on the local machine)
