for link in `cat picm`
do
    id=$(curl -s $link | egrep -o  'oldid=[0-9]{5,6}' | egrep -o '[0-9]{5,6}' | sort -u)
    if [ ! -f ./people/$id/$id.html ] 
    then
        echo "link: $link\tid: $id" >> mk_people.log
        mkdir -p ./people/$id
        curl -s $link > ./people/$id/$id.html
    fi
    if [ -z $id ]
    then
        echo "ERROR :: $link has no ID!" >> mk_people.log
    fi
done
