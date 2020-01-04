import { Component, OnInit } from '@angular/core';

import { WizDataService } from '../../wiz-data.service';
import { debug } from 'util';
import { Input } from '@angular/core';

@Component({
  selector: 'app-editions-card',
  templateUrl: './editions-card.component.html',
  styleUrls: ['./editions-card.component.scss']
})

export class EditionsCardComponent  {
  // implements OnInit

  @Input() src;
  constructor(
    private wizDataService: WizDataService
  ) { }

  ngOnInit() {
    console.log(this.src);
  }

}
