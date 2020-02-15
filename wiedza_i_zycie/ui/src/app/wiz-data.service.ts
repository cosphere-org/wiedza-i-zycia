import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class WizDataService {

  myVariable: any;

  constructor(
    private http: HttpClient) {
      this.getWizJson().subscribe(data => {
        console.log(data);
    });
}

public getWizJson() {
  return this.http.get("/assets/editions.json");
}

public getData(){
  this.getWizJson().subscribe(data => {
    console.log(data);
    return data;
  });
  // debugger;
}

public getEdition(number){
  this.getWizJson().subscribe(data => {
    console.log(data[number])
    // return data[number];
  });
}

}
