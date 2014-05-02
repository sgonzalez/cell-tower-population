#!/usr/bin/ruby

#########################
### Santiago Gonzalez ###
#########################

require 'net/http'

def process_line line, poly_out_file, pops_out_file
  split_line = line.split(' ', 2)
  polygon_id = split_line[0]
  points = split_line[1].scan(/POINT\((-?\d+\.\d+) (-?\d+\.\d+)\)/)

  points.each do |vertex|
    print polygon_id
    print ", "
    print vertex[0]
    print ", "
    print vertex[1]
    puts ""
    poly_out_file.write("#{polygon_id}, #{vertex[0]}, #{vertex[1]}\n")
  end
  
  puts ""
end






############################
## PROGRAM EXECUTION START

# take input file argument
if ARGV.length != 1
  puts "Usage: ./polygon_processor.rb [results file]"
  exit 1
end
filename = ARGV[0]

# parse file line by line
File.open(filename, "r") do |file|
  File.open("OUTPUT/parsed_polygons.csv", 'w+') do |poly_out_file|
    File.open("OUTPUT/polygon_populations.csv", 'w') do |pops_out_file|
      file.each do |ln|
        process_line ln, poly_out_file, pops_out_file
      end
    end
  end
end

exit 0
