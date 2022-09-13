<br />
<p align="center">
  <h1 align="center">Web Scraping</h1>
</p>
<p align="center">
  Python Tool Kit for Web Scraping
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

Simple code to scrap data from websites
<br />
<br />

## Installation

To get a local copy up and running follow these simple steps.

### Set up environment

```
conda env create -f environment.yml

conda activate web_scraping
```

### Visual Studio Code

After running the code above in Terminal, you still have to select the environment in VSCode. Click `F1`, select `Python: Select Interpreter`, click `Enter` and select the one that has `web_scraping` in brackets. If you don't see the environment in the list, reload VS Code.

<br />
<br />

## Run

In order to generate the dummy dataset run the following jupyter notebook:
   ```sh
   src/main.ipynb
   ```

<br />
<br />

## Project Structure

The project is composed of a main notebook.

Other files such as helper.py are used as auxiliary code to assist this main notebook.

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
    ├── src          <- Source code as Jupyter notebooks
    │
    ├── environment.yml           <- YAML file to create conda environment to run the project
   
</code></pre>

<br />
<br />

### Built With

* [Python 3.10](https://www.python.org/)
* [Jupyter Notebook](https://jupyter.org/ )

