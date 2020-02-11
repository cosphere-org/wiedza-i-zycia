import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditionsCardComponent } from './editions-card.component';

describe('EditionsCardComponent', () => {
  let component: EditionsCardComponent;
  let fixture: ComponentFixture<EditionsCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditionsCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditionsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
