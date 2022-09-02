# Scrapy Projects
Scrapy Tutorial and Project Repository.

## Table of Contents

- [Scrapy](#scrapy-projects)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Scrapy Shell](#scrapy-shell)
  - [Scrapy Tutorial](#scrapy-tutorial)

## Installation

Installation of Dependencies:
```bash
conda create -n scrapy-env python=3.8
conda activate scrapy-env
conda install -c conda-forge scrapy
```

## Scrapy Shell
Scrapy provides a web-crawling shell called as _Scrapy Shell_, that developers can use to test their assumptions on a site's behavior. You can use the Scrapy shell to see what components the web page returns and how you can use them to your requirements.

Open your command line and write the following command:
```bash
scrapy shell
```

You have to run a crawler on the web page using the `fetch` command in the Scrapy shell. A crawler or spider will go through the webpage and download its text and metadata.

```
fetch('https://google.com/')
```

>Note: Always enclose URL in quotes, both single and double quotes work.

The crawler returns a __response__ which can be viewed by using the `view(response)` command on the shell:

```bash
view(response)
```

You can also view the raw HTML script by using the following command in Scrapy Shell:

```bash
print(response.text)
```

## Scrapy Tutorial

To activate scrapy spider, under project base:

```bash
scrapy crawl <spider-name>
```

To export results:

```bash
scrapy crawl <spider-name> -O [<filename.csv>, <filename.json>]
```
