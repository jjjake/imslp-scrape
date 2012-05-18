# This script crawls through http://imslp.org/wiki/Category:People
# and returns each resulting page. 
#
# Results per page: 200
# Each results page contains a link to a "Person" or composer.

# Insert the 'seed' URL below. 
URL='http://imslp.org/wiki/Category:People'

while true
do
    URL=$(lwp-request -o links $URL | egrep -o 'http://imslp.org/.*People\&subcatfrom.*subcategories$' | sort -u)
    echo $URL
done
