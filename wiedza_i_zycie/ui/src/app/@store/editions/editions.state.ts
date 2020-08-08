
import { Edition } from './editions.model';

export interface EditionsState {

  allEditions: Edition[];
  
  filteredEditions: Edition[];

  selectedEdition: Edition;

  setProgressBar: boolean;
}
