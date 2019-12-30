import { Component, OnInit } from '@angular/core';
import { WizDataService } from '../wiz-data.service';

@Component({
  selector: 'app-main-view',
  templateUrl: './main-view.component.html',
  styleUrls: ['./main-view.component.scss']
})
export class MainViewComponent implements OnInit {

  wizData;

  constructor(
    private wizDataService: WizDataService
  ) { }

  ngOnInit() {
    this.wizDataService.getWizJson().subscribe(data => {
      console.log(data[0]);
      this.wizData = data;
    });
  }

  getData(){
    this.wizDataService.getWizJson().subscribe(data => {
      // console.log(data);
      this.wizData = data;
      // return data; 
    });
    
  }

}
