echo "Generate kapp-controller marker............."
echo "marker: $(git rev-parse --short HEAD)" > kapp-marker
echo "Adding kapp-controller marker to repo............."
git add kapp-marker