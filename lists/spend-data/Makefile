
download = ( mkdir -p $(1) && \
  cd $(1) && \
	curl https://www.gov.uk/government/publications/$(2) \
	| grep uploads \
	| grep '.csv"' \
	| sed 's/<a href="/https:\/\/www.gov.uk\//' \
	| sed 's/">//' \
	| xargs -n1 -P4 curl -O \
	&& cd .. )

all: amounts.csv

download-2016-2017:
	[[ -e ./2016-2017/DfE_Spend_`date -v-1m "+%B_%Y"`.csv ]] ||\
	$(call download,2016-2017,dfe-and-executive-agency-spend-over-25000-2016-to-2017)

download-2015-2016:
	[[ -e ./2015-2016/DfE_Spend_March_2016.csv ]] ||\
	$(call download,2015-2016,dfe-and-executive-agency-spend-over-25000-2015-to-2016)

suppliers.csv: download-2016-2017 download-2015-2016
	[[ -e $@ ]] || \
	ls 20*/DfE*.csv \
	| xargs -n1 csvcut -c Supplier -e ISO-8859-1 \
	| iconv -f ISO-8859-1 -t UTF-8 \
	| grep -v Supplier \
	| sort -u \
	| sed 's/^$$/supplier/' \
	> $@

transactions = (echo "supplier,amount" &&\
	ls $(1)*/DfE* \
	| xargs -n1 csvcut -c Supplier,Amount -e ISO-8859-1 \
	| iconv -f ISO-8859-1 -t UTF-8 \
	| sed 's/Supplier,Amount//' \
	| awk NF )

transactions-2015-2016.csv: suppliers.csv
	$(call transactions,2015) \
	> $@

transactions-2016-2017.csv: suppliers.csv
	$(call transactions,2016) \
	> $@

amounts = csvsql --query \
	'select d.supplier,round(sum(d.amount),2) as "amount-$(1)" from "transactions-$(1)" as d group by d.supplier order by amount desc' \
	transactions-$(1).csv

amounts-2015-2016.csv: transactions-2015-2016.csv
	$(call amounts,2015-2016) \
	> $@

amounts-2016-2017.csv: transactions-2016-2017.csv
	$(call amounts,2016-2017) \
	> $@

amounts.csv: amounts-2015-2016.csv amounts-2016-2017.csv
	csvjoin --outer -c supplier amounts-2015-2016.csv amounts-2016-2017.csv \
	> $@

clean:
	rm -f supplies.tsv
	rm -f transactions*.csv
	rm -f amounts*.csv
