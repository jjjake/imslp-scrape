for link in `cat people_pages.txt`
do
    id=$(curl -s $link | egrep -o  'oldid=[0-9]{6}' | egrep -o '[0-9]{6}' | sort -u)
    mkdir -p ./people/$id
    curl -s $link > ./people/$id/$id.html
done
