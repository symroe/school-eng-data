
download = curl https://www.gov.uk/government/publications/$(1) \
	| grep uploads \
	| grep '.csv"' \
	| sed 's/<a href="/https:\/\/www.gov.uk\//' \
	| sed 's/">//' \
	| xargs -n1 -P4 curl -O

all: suppliers.tsv

download-2016-17:
	[[ -e DfE_Spend_`date -v-1m "+%B_%Y"`.csv ]] ||\
	$(call download,dfe-and-executive-agency-spend-over-25000-2016-to-2017)

download-2015-16:
	[[ -e DfE_Spend_March_2016.csv ]] ||\
	$(call download,dfe-and-executive-agency-spend-over-25000-2015-to-2016)

suppliers.tsv: download-2016-17 download-2015-16
	[[ -e $@ ]] || \
	ls DfE*.csv \
	| xargs -n1 csvcut -c Supplier -e ISO-8859-1 \
	| iconv -f ISO-8859-1 -t UTF-8 \
	| grep -v Supplier \
	| sort -u \
	| sed 's/^$$/supplier/' \
	> $@
