import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { WizDataService } from '../wiz-data.service';

@Component({
  selector: 'app-editions-grid',
  templateUrl: './editions-grid.component.html',
  styleUrls: ['./editions-grid.component.scss']
})
export class EditionsGridComponent implements OnInit {

  @Output() editionSelected: EventEmitter<string> = new EventEmitter<string>();

  editions;

  constructor(
    private wizDataService: WizDataService
  ) { }

  ngOnInit() {
    this.wizDataService.getWizJson().subscribe(editions => {
      this.editions = editions;
    });
  }

  getPath(){

  }

}
