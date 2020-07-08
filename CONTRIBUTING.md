# Contribution Guidelines

So you want to help us out? First of all, thank you!
There are few rules that we have so anyone can participate while maintaining a good workflow, teamwork, and clean code.
These are likely to get modified or added stuff to it, check them regularly.

To contribute to the bot development, you need to be on the official TryHackMe Discord server. https://discord.gg/tryhackme


## Github

### Issues
- Feel free to ask to be assigned to an issue or to do an issue that no one is assigned to.
- You can create issues, please provide as many details as possible and cut the issue into tasks. (tasks are the checklists that you can put in an issue's desc)
- It is pointless to work on an issue that is assigned to someone else.
- Use tags and labels.

### Pull Requests
- Link the issue you are resolving in the description, if part of that issue was not possible to fix/complete, say so and why in the description.
- One commit per implementation. You can merge more than one commit. (I'd rather not to avoid merge conflict, but it is ok if you do)
- The use of the internal libraries is obligatory. You are free to add to it if it does not cover a scenario that you need. (Please run it by the lead devs first as they are used everywhere)
- Any spelling mistakes will lead to immediate rejection of pull requests.
- A code that does not compile or crashes is a code that does not get merged. 
- If a PR is refused it will most likely have a justification in the comments, though it is not obligatory. It is not because a PR has been refused that it won't ever be accepted.
- Do not spam dev leads to get reviewed quicker.
- Use tags and labels.


## Code formatting and structure

### General
- Please, respect the current code architecture; if you think something should change feel free to let us know.
- Personal initiative is good, but for the sake of working together in good condition, let other people know what you do or want to do before doing it.

### Naming convention
- We will prefer using underscores for function names such as my_function.
- For variables, we will use the following myVar or my_var.
- Try and use prefixes to make your variables clear, s_ is used for strings from the string.json file and c_ for the config file.
- A code with unclear function and variable names will be refused.

### Commands
- Every command must have a description.
- If the command is staff only, it needs to have the hidden value set to true.
- If there are arguments, the command will have a usage field.
- You must use the "command" system from the internal libs to handle sanitizing, roles permissions and context restriction.

### Documenting and comments
- You need to document every function that is not a command using ''' blocs.
- Try to comment your code using comments as much as possible.
- A code that is not documented is a code that gets refused on review. 

### Config and data
- Do *NOT* push data and config files. They are in the gitignore for a reason. If you need something added to it, specify it in the description of the Pull Request. If it is sensitive, the person in charge of reviewing the PR will get back to you using Discord.
- Configs go in the "config.json" file. (see config file for path).
- Any text destined to users has to go in the "strings.json" file. (see config file for path).
- Any data that needs to be written locally goes in the appropriate folder, in a new file. (use the config file for path).

### Display
- Any output longer than 10 lines should be paged, i.e. a total page count should be included in the output and a page argument.
should be included in the bot command.
- Commands output (other than a few exceptions) HAVE to be generated using the official embed system.

### The Fun cog
- We want to keep the bot mostly practical. We do like the fun cog, but we will ask you not to focus on it too much.
- Most commands in it are memes, memes die, don't be surprised if a command in the fun cogs gets removed for lack of use. (We will try not to delete anything, just comment the command)

### Credentials
- While implementing a feature, if it requires an account on a specific platform you are free to try your code on yours. Please let us know before asking for the pull request so that we can set up an official account for the bot on the said platform.

### Tests
- You will not have access to the official instance of the bot.
- Feel free to recreate your TryHackMe discord and bot in a private server and change the values in the config of your local instance of the bot to test your code.
- There is a test server that you can join and invite your bots on, we will provide you with the "config.json" file needed for the instance to work on the server. Also the bot's permissions are the same as on the official server.

### Permissions
- If any aditionnal permission is required, contact a dev lead before coding anything so that a decision can be taken.
- If you abuse or try to abuse of the bot permissions on the official or test server, there will be consequences.


## Credits

At TryHackMe we take credits seriously. If you have contributed to the bot, let people know by adding your name and the features you have implemented at the bottom of the list on the README.md.
You can also add more features beneath your name if you contribute again in the future.


## Questions

If you have any problems or questions, please come talk to us on Discord. This is where the community is gathered and we have channels dedicated to the bot.