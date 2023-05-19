INSTALL_DIR="/usr/local/bin"
curl -O https://files.pythonhosted.org/packages/e8/04/4a80ddcfd1e36540198cc42faf735e76f636f08a50b87462c4d09bf9730b/musiccli-1.2.0.tar.gz

tar -xzvf musiccli.tar.gz
mv musiccli "$INSTALL_DIR"


case "$SHELL" in
  */bash*)
    echo 'alias mcli="python -m musiccli"' >> ~/.bashrc
    source ~/.bashrc
    ;;
  */zsh*)
    echo 'alias mcli="python -m musiccli"' >> ~/.zshrc
    source ~/.zshrc
    ;;
  */fish*)
    echo 'alias mcli "python -m musiccli"' >> ~/.config/fish/config.fish
    ;;
  *)
    echo "Unsupported shell: $SHELL"
    exit 1
    ;;
esac

rm musiccli.tar.gz

echo "MusicCLI has been installed successfully. You can now use 'mcli [SONG_NAME]'
to run the command."