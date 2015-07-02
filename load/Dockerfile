# Build based on virtuoso container in order to have access to virtuoso's
# isql command.
FROM caprenter/automated-build-virtuoso
ADD load.sh /load.sh
ADD import.sql /import.sql
CMD /load.sh
