# CTFd-Cooldown-Plugin

This CTFd plugin introduces a dynamic **challenge cooldown mechanism** designed to add an extra layer of strategy to your Capture The Flag competition. When a team solves a challenge, a **random team that hasn't solved it yet** is temporarily blocked from submitting it, simulating a "cooldown" period.


## ✨ Features
- ⏱️ **Cooldown Logic**  
  When a challenge is solved, a random team that hasn't solved it is blocked from submitting it for a configurable amount of time (default: 3 minutes).

- 🔁 **Automatic Unblocking**  
  After the cooldown expires, blocked teams can try submitting again.

- 🧠 **Fair Random Selection**  
  Victim teams are chosen `randomly` in hopes a team does not get frozen twice for the same challenge!

- 🛑 **Rejection Feedback**  
  Blocked teams receive a message instead of a silent fail or generic error.


## 🧩 How It Works

1. A team solves a challenge correctly.
2. The plugin selects one **random team** (that hasn’t yet solved the challenge) and blocks them from submitting it for `X` minutes.
3. If a blocked team attempts to submit during this time, they receive a message instead:

    ```
    Submission for this challenge was blocked by the K3rnelDumps. Try again in 102 seconds ;)
    ```

4. Once the cooldown expires, submission is re-enabled automatically.

## ⚙️ Configuration

You can configure the cooldown duration directly in the plugin source code:

```python
minutes = 3  # Set to your desired cooldown time
```

## 📦 Installation
1. Move the file to the plugins folder.
    ```bash
    cp -r your_plugin_folder/ CTFd/plugins/challenge_cooldown/
    ```

2. Restart the CTFd server.

## 🔐 Notes
* Only teams that haven’t solved the challenge are considered for blocking.
* The plugin overrides the default challenge_attempt route to provide a custom message.
* Blocked submissions are treated as **incorrect** to preserve red coloring in the UI.
Cooldown state is stored in memory. Restarting the server clears all active cooldowns.

## 🤝 Contributing
You're welcome to fork this project and contribute! Ideas for improvement include:
* Adding an admin UI to control plugin behavior.

## 🧠 Example Use Case
This plugin is perfect for time-pressure or sabotage-style CTFs, where strategic delays can affect scoring and create tension between teams.