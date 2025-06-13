base_folder="$1"
mode="$2"

if [ -z "$base_folder" ]; then
    echo "Usage: bash launch.sh <base_folder> [-r|-a]"
    echo "base_folder: Path to the folder containing the data files."
    echo "mode: -r for range processing, -a for azimuth processing, or leave empty for both."
    exit 1
fi

# Range
chirp_path="$base_folder/reference_chirp_p60tx_p60rx.dat"
data_path="$base_folder/raw_data.npy"
topo_path="$base_folder/topo.npy"
output_path="$base_folder/range_compressed.npy"
image_path="$base_folder/range_image.png"

# Azimuth
az_data_path="$base_folder/range_compressed.npy"
az_output_path="$base_folder/processed_data.npy"
az_image_path="$base_folder/compressed.png"

if [ "$mode" = "-r" ]; then
    echo "Running range processing..."
    python ./src/range.py --chirp_path $chirp_path --data_path $data_path --topo_path $topo_path --output_path $output_path --image_path $image_path
elif [ "$mode" = "-a" ]; then
    echo "Running azimuth processing..."
    python ./src/azimuth.py --data_path $az_data_path --output_path $az_output_path --image_path $az_image_path
elif [ -z "$mode" ]; then
    echo "Running range processing..."
    python ./src/range.py --chirp_path $chirp_path --data_path $data_path --topo_path $topo_path --output_path $output_path --image_path $image_path
    echo "Running azimuth processing..."
    python ./src/azimuth.py --data_path $az_data_path --output_path $az_output_path --image_path $az_image_path
else
    echo "Invalid mode: $mode"
    echo "Usage: bash launch.sh <base_folder> [-r|-a]"
    exit 1
fi