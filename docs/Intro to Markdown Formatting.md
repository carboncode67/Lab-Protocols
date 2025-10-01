mkdocs uses mardown (.md) files to render text in a consistent and visually pleasing manner. Markdown is a protocol for formatting text that is (mostly) interchangeable between software programs.
Here are a few key shortcuts to use when making web pages.

## Headings
Headings and subheadings can be created using the ```#```, where the number of ```#``` symbols represents the heading level, for example ```## Title``` would be rendred as
## Title
wherea as ```### Title``` would be
### Title

## Bullets and Lists
```*```, ```1.``` and ```- [ ]``` can be used to start a list.

For example, 

* First task

or 

1. Task One

and

- [ ] Checklist 
- [x] add an "x" between the brackets to check the box

They can be used together to make nested lists, for example,
```md
1. task one
    * Sub tasks 
2. task 2,
    - [ ] remember to check the thing
```
renders as:

1. task one
    * Sub tasks 
2. task 2,
    - [ ] remember to check the thing

### Callouts
To draw attention to peices of information, or make make callapsable notes to save space, mkdocs supports callouts, which can be created with ```???+ 'keyword'```, or ```!!! 'keyword'```,where keyword defines the type of callout. For example: if I wanted to make a note about specific instrument settings, 
```md
!!! note
    This is an important factoid
```
would render as: 

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.