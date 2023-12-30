# Ghost v3
A rewrite of the popular Discord selfbot, Ghost.  
**FYI:** There are no raid commands in this selfbot and we will not be adding any.  

### How to use
> Make sure you have Python installed.  
> Download the latest release or the source code.  
> Run `ghost.py`.  

### Todo list
> - [ ] Bring command amount to similar amount as old ghost
> - [ ] Add nitro sniper
> - [ ] Add giveaway joiner

### Support
> If you need help please read our [Wiki](https://github.com/ghostsb/ghost/wiki) and if you are still in need of support please create an issue.  
> *Please do not ask for help in Ben's discord server, we will not help with ghost!*

### Improper Token Passed
- If you encounter an issue where it says `Improper token passed` but you're 100% sure it's the right token. It's because of discord.py-self
- Recently, Discord made a change in the API were some requests need a build number
- The current `pypi` version of discord.py-self has a patched version to fetch the number. However, the development version doesn't
- To install the development version simply uninstall your current version of `discord.py-self` by inputting
- `pip install discord.py-self`
- Then execute:
- `pip install git+https://github.com/dolfies/discord.py-self@master#egg=discord.py-self`
- Make sure you have Git installed!
- Once installed, re-run `Ghost.py` and it should be fixed!
