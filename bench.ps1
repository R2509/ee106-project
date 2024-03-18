clear;
for ($i = 0; $i -gt $1; $i++) {
    Write-Output 'summary-bench --file ./small_dataset.csv -se 1 -te "2018-04-01 00:01:00" -n 10 -m thread; exit' | python main.py
}
