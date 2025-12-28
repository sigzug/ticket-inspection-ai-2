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

// Submit request for running the model.
export interface UseModelRequest {
  line: string;
  departure_station: string;
  arrival_station: string;
  only_standing: boolean;
  departure_time: Date;
}

// The backend response shape isn’t specified; keep it generic.
export type UseModelResponse = Record<string, any>;
