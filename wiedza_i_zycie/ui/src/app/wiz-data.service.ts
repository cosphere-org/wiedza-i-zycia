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

public getEditions(){
  this.getWizJson().subscribe(Editions => {
    console.log(Editions);
    return Editions;
  });
  // debugger;
}

public getEdition(number){
  this.getWizJson().subscribe(data => {
    console.log(data[number])
    // return data[number];
  });
}

public getArticles(){
  let articles = []
  this.getWizJson().subscribe(Editions => {
    // Editions.forEach(edition => {
      
    // });
    console.log(Editions);
    // return data;
  });
}

}
