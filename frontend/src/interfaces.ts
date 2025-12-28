export interface Categories {
  only_standing: string[];
  checked: string[];
  wagon: string[];
  notes: string[];
  line: string[];
  departure_station: string[];
  arrival_station: string[];
}

export interface CategoriesResponse {
  categories: Categories;
}
