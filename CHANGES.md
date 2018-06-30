## Version 0.2

(next version)

### Version 0.1.15 (2018-06-30)

* Support Sphinx's doc/ref directives for relative links ([#16](https://github.com/miyakogi/m2r/pull/16))

### Version 0.1.14 (2018-03-22)

* Implement markdown link with title

### Version 0.1.13 (2018-02-14)

* Catch up sphinx updates

### Version 0.1.12 (2017-09-11)

* Support multi byte characters for heading

### Version 0.1.11 (2017-08-30)

* Add metadata for sphinx
* Add `convert(src)` function, which is shortcut of `m2r.M2R()(src)`

### Version 0.1.10 (2017-08-15)

* Include CHANGES and test files in source distribution

### Version 0.1.9 (2017-08-12)

* Print help when input_file is not specified on command-line

### Version 0.1.8 (2017-08-11)

* Update metadata on setup.py

### Version 0.1.7 (2017-07-20)

* Fix undefined name error (PR #5).

### Version 0.1.6 (2017-05-31)

* Drop python 3.3 support
* Improve image_link regex (PR #3)

### Version 0.1.5 (2016-06-21)

* Support multiple backticks in inline code, like: ```backticks (``) in code```

### Version 0.1.4 (2016-06-08)

* Support indented directives/reST-comments
* Support role-name after backticks (`` `text`:role: style``)

### Version 0.1.3 (2016-06-02)

* Remove extra escaped-spaces ('\ ')
    * before and after normal spaces
    * at the beginning of lines
    * before dots

### Version 0.1.2 (2016-06-01)

* Add reST's `::` marker support
* Add options to disable emphasis by underscore (`_` or `__`)

### Version 0.1.1 (2016-05-30)

* Fix Bug: when code or link is placed at the end of line, spaces to the next word is disappeared

## Version 0.1 (2016-05-30)

First public release.
