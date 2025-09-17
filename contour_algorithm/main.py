import create_files_shoes
import contour
import active_contour_snake
import distance_extremities
import contact_with_locations

if __name__ == '__main__':
    create_files_shoes.main()
    contour.main()
    active_contour_snake.main()
    distance_extremities.main()
    contact_with_locations.main() 
    print("Pipeline completed successfully (without final contact analysis)")





