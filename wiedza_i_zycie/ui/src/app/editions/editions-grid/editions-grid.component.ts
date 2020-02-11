import { Component, OnInit } from '@angular/core';
import { WizDataService } from '../wiz-data.service';

@Component({
  selector: 'app-editions-grid',
  templateUrl: './editions-grid.component.html',
  styleUrls: ['./editions-grid.component.scss']
})
export class EditionsGridComponent implements OnInit {

  editionsData;

  constructor(
    private wizDataService: WizDataService
  ) { }

  ngOnInit() {
    this.wizDataService.getWizJson().subscribe(data => {
      console.log(data[0]);
      this.editionsData = data;
    });
  }
  
  getPath(){

  }

}
