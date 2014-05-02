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
  
  ######### FORMAT DATA AND CREATE INITIAL HTTP REQUEST
  geometry = { "geometryType" => "esriGeometryPolygon", "spatialReference" => {"wkid" => 4326}, "features" => [ { "geometry" => {"rings" => [ points ] }, "attributes" => {"Id" => 43, "Name" => "Feature 1"} } ] }
  geometry = geometry.to_s
  uri = URI.parse("http://sedac.ciesin.columbia.edu/mapservices/arcgis/rest/services/sedac/GPW/GPServer/PopStatsFeatures/submitJob?Input_Feature_Set=#{URI.escape(geometry)}")
  response = Net::HTTP.get_response(uri)
  
  results_location = ((response.to_hash)['location'])[0]
  puts results_location
  
  ######### LOOP WHILE DATA IS BEING PROCESSED BY SERVER
  finished = false
  num_polls = 0
  stuck = false
  while !finished
    
    if num_polls > 50 # program got stuck
      stuck = true
      break
    end

    results_response = Net::HTTP.get_response(URI.parse(results_location))

    results_body = results_response.body
    status = results_body.match(/<b>Job Status:<\/b> (.*)<br\/><br\/>/)
    
    puts status[1]

    if status[1] == "esriJobSucceeded"
      finished = true
      break
    end
    
    num_polls += 1

    sleep 10
  end
  
  ######### HANDLE STUCK PROGRAM
  if stuck
  #   last_line = 0; poly_out_file.each { last_line = poly_out_file.pos unless poly_out_file.eof? }; poly_out_file.seek(last_line, IO::SEEK_SET) # "remove" last line from poly_out_file
  #   process_line line, poly_out_file, pops_out_file
    return
  end
  
  ######### PULL DATA FROM SERVER
  final_location = results_location + "/results/pop_stats_features_2"
  final_response = Net::HTTP.get_response(URI.parse(final_location))
  
  
  ######### PARSE AND SAVE DATA
  population = (final_response.body.gsub!(/\s/, '').gsub("\n",'').match(/POPULATION05:(\d+(\.\d+))<br\/>/))[1]
  puts "ID #{polygon_id}: #{population}"
  pops_out_file.write("#{polygon_id}, #{population}\n")
  
  
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