import { Component, OnInit } from '@angular/core';

import { WizDataService } from '../wiz-data.service';
import { debug } from 'util';
import { Input } from '@angular/core';


@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss']
})

export class CardComponent implements OnInit {

  @Input() src;
  constructor(
    private wizDataService: WizDataService
  ) { }

  ngOnInit() {
    console.log(this.src);
  }

}
