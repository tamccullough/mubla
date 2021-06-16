# Mubla
## Photo Album

None of us should be storing our photos and videos in the cloud.
Or atleast we should avoid it as much as possible. I don't believe we can trust big tech with our personal lives.

Personally, I have my files stored on an SSD(with multiple backups) so that I can access the files on any device within my home using this repository.

Originally we were using some third party apps to browse our photo/video library, but I didn't fully trust what those apps may have been accessing.

So I made Mubla.

## Setup

*This has been made using Linux, so you may need to add some extra code to run it on Windows or Mac*
- change the path in the main.py file to your photos path
  - `root_folder = '/your/photos/path'` to something that references your file structure
- setup the virtual environment and activate it
  - `python -m venv <env dir>`
  - `source /<env dir>/bin/activate`
- run `flask run --host=0.0.0.0` (without the host argument it will only be available on the local machine)

#### Directory Setup;

photos/year/month/day/<filename>

- year
  - month
    - day
      - file

#### Example;

- photos(root)
  - 2020(year)
    - 01(month)
      - 01(day)
        - video 1(file)
        - video 2(file)
    - 02(month)
      - 01(day)
        - photo1(file)
        - photo2(file)
        - video1(file)
 
## Recommendations

Organize your photos/videos in the same manner to use this flask app without problems.
 
Take the time to set it up correctly. These are your memories afterall.

If you choose to make the directory structure different, you will then need to edit the main.py file.
