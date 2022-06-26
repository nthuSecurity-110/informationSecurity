# Information Security Lab 110 Repository 💻

## Git 101 ✅
### Setup
- Run `git clone https://github.com/nthuSecurity-110/informationSecurity.git`
- Run `pip install python-nmap`
- Run `pip install multiprocess`
- Run `pip install treelib`
- Run `python main.py` in Windows to execute the program.

### Modifying Files
- Run `git checkout islab/[your_name]`
- Make your changes
- Run these commands in order:
    1. `git add --a`
    2. `git status` --> optional, to check the modified files
    3. `git commit -m "enter your commit message"`
    4. `git push origin islab/[your_name]`
- Branch names:
    - 家秀：islab/chelsea
    - 家燕：islab/jessica
    - 晴雯：islab/michelle
    - 徐祈：islab/jose
    - 妍廷：islab/sakura

### To get the latest official development update
- Run `git pull origin main`

### Additional git commands (avoid using these commands if unnecessary)
- git restore [file_name] --> restore a file from another commit.
- git reflog --> show updates on the branch and the current HEAD.
- git checkout [commit_id] --> switch to another commit.

### IMPORTANT NOTE
- Remember to make commits and push to your own branch, not to main :)
- We will then run a test to make sure that the commits you have made can run without any errors.
- After the test:
    - If no errors --> create a pull request (PR) --> person in charge will merge to main branch
    - If error found --> fix in your respective branch --> re-push

## When Coding 🔥
- Use Class in different files --> bundling functionalities together to make the overall development process neater and easier to understand.
- For each classes:
    - Provide a documentation (brief explanation) about the class. If possible, include:
        1. Short description about the class' functionality.
        2. The commands (functions in the class) and a short description.
- For each class methods:
    - Provide a documentation about the function. If possible, include:
        1. Brief explanation about what the function does.
        2. Parameters (what are the inputs, input types).
        3. Return value.
- Comments are very welcomed when coding!

## 大家加油！(ง •_•)ง
