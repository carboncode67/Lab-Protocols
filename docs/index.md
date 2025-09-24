# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## To contribute to this documentation:
* use `pip install mkdocs mkdocs-material` to install mkdocs and the Material theme
* Open a terminal window in the directory where you wish to download the repostiory and enter `git clone https://github.com/carboncode67/Lab-Protocols.git`
* enter `cd Lab-Protocols`.
* Create a new .md document in the docs folder inside "Lab-Protocols/docs. If adding multiple documents, you can create a sub directory in the docs folder and add .md docs there.
* If you want to see your changes live, you can enter `mkdocs serve` and navigate to the displayed url to see updates and errors as you work.
    * If you are including images in the documentation, and your new doc .md file is in the root docs directory add them to `Lab-Protocols/docs/assets`, and then link to them in your documentation using `"![image](assets/image.png)"` (without the quotation marks). If your new doc is in its own folder, add the images to that folder and reference directly. 
* Once changes are made, use the following commands (or github desktop) to push the changes to the main repo.
```sh
git add .
git commit -m "Add/Update docs: <describe updates added here>"
git push origin main
```
* run `mkdocs gh-deploy` to deploy the site.
Done!


## General mkdocs Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file (Be careful editing this ).
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
