for link in `cat people_pages.txt`
do
    id=$(curl -s $link | egrep -o  'oldid=[0-9]{5,6}' | egrep -o '[0-9]{5,6}' | sort -u)
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
