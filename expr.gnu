set xlabel 'Experience'
set ylabel 'Number of Jobs completed'
set grid
set title 'Number of jobs finished Vs Experience'
set xr[0:3]
set yr[0:15]
plot "expr1.txt" u 1:2 with lp t "experience counts : run 1",\
      "naive1.txt" u 1:2 with lp t "Naive : run 1"


plot "expr2.txt" u 1:2 with lp t "experience counts : run 1",\
    "naive2.txt" u 1:2 with lp t "Naive : run 2"
