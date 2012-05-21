# Create a directory for each person page and download it's HTML into said directory.
# Input: people_page_urls.txt, a list of URLs to each person page.
# Output: people/{ID}/{ID}.html + tab-delimited 2 column text file (id, url).

for link in `cat people_page_urls.txt`
do
    id=$(curl -s $link | egrep -o  'oldid=[0-9]{5,6}' | egrep -o '[0-9]{5,6}' | sort -u)
    echo "$id\t$link"
    if [ ! -f ./people/$id/$id.html ] 
    then
        mkdir -p ./people/$id
        curl -s $link > ./people/$id/$id.html
    elif [ -z $id ]
    then
        echo "ERROR :: $link has no ID!" >> mk_people.log
    else

        echo "ERROR :: $link couldn't create item!" >> mk_people.log
    fi
done
