<br />
<p align="center">
  <h1 align="center">SWIFT codes Scraper</h1>
</p>
<p align="center">
  Python Tool for Scraping SWIFT/BIC codes
  <br />
  <br />
  <br />
</p>




<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
    <li>
      <a href="#run">Run</a>
    </li>
    <li><a href="#project-structure">Project Structure</a></li>
    
  </ol>
</details>
<br />
<br />


<!-- ABOUT THE PROJECT -->
## About The Project

This code scraps public available SWIFT codes and its metadata from [theswiftcodes.com](https://www.theswiftcodes.com/).

<br />
<br />

## Installation

To get a local copy up and running follow these simple steps.

### Clone repository

In your terminal, change the current working directory to the location where you want the cloned directory.

As shown below, type git clone in the terminal, paste the Github repository URL, and press “enter” to create your local clone. 

```
git clone https://github.com/Tax-Justice-Network/swift_codes_scraper.git
```

### Set up environment

```
conda env create -f environment.yml

conda activate swift_codes_scraper
```

### Visual Studio Code

After running the code above in Terminal, you still have to select the environment in VSCode. Click `F1`, select `Python: Select Interpreter`, click `Enter` and select the one that has `swift_codes_scraper` in brackets. If you don't see the environment in the list, reload VS Code.

<br />
<br />

## Run

To scrape SWIFT data automatically, without interaction, you can issue (launch with `--help` for a detailed explanation of each argument)
```sh
python ./src/swift_scrapper.py --full_bank_info --output_path ../data/final/swifts.jsonl
```

<br />
<br />

## Project Structure

The project is composed of a main notebook named swift_scraper.py.

<br />

This is the project structure followed by this project:
<pre><code>

  
├── LICENSE 
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── final          <- Final data and results
│   ├── processed      <- Intermediate datasets
│   └── raw            <- The original, immutable data dump
│
├── docs               <- Documents of interest for this project
│
├── src                <- Source code as Jupyter notebooks and main scripts.
│
├── environment.yml    <- YAML file to create conda environment to run the project
   
</code></pre>

<br />
<br />

### Built With

* [Python 3.10](https://www.python.org/)
* [Jupyter Notebook](https://jupyter.org/ )

