import { Component, OnInit, HostListener } from '@angular/core';

// import { WizDataService } from '../wiz-data.service';
import { debug } from 'util';
import { Input } from '@angular/core';
import { NavCommunicationService } from 'src/app/shared/nav-communication.service';


@Component({
  selector: 'app-editions-card',
  templateUrl: './editions-card.component.html',
  styleUrls: ['./editions-card.component.scss']
})

export class EditionsCardComponent  {
  // implements OnInit

  @Input() src
  @Input() date 

  constructor(
    // private wizDataService: WizDataService
    private navCommunicationService: NavCommunicationService
  ) { }

  ngOnInit() {
    // console.log(this.src);
    // console.log(this.editionProps);
  }

  showDetalis(){
    this.navCommunicationService.toggle();
  }

}
