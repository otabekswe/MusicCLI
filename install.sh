if pip show musiccli &> /dev/null; then
    echo "Performing package update.."
    pip install --upgrade musiccli
else:
    echo "Initiating package installation..."
    pip install musiccli
fi

case "$SHELL" in
  */bash*)
    echo "alias mcli='python -m musiccli'" >> ~/.bashrc
    echo "alias mcli='python3 -m musiccli'" >> ~/.bashrc
    source ~/.bashrc
    ;;
  */zsh*)
    echo "alias mcli='python -m musiccli'" >> ~/.zshrc
    echo "alias mcli='python3 -m musiccli'" >> ~/.zshrc
    source ~/.zshrc
    ;;
  */fish*)
    echo "alias mcli='python -m musiccli'" >> ~/.config/fish/config.fish
    echo "alias mcli='python3 -m musiccli'" >> ~/.config/fish/config.fish
    ;;
  *)
    echo "Unsupported shell: $SHELL"
    exit 1
    ;;
esac

echo "MusicCLI has been installed successfully. \nYou can now use 'mcli [SONG_NAME]' to run the command."
