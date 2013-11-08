for i in {5..11000..1000}
do
    echo $i
     command="sed -i 's/CUSTOMER_POOL_SIZE = [0-9]*/CUSTOMER_POOL_SIZE = $i/g' perfsim.config"
     eval $command
     python basic_sim.py
done
