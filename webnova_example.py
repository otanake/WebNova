"""
WebNova - Simple Event-Driven Real-Time Processing Engine
A configurable event-driven architecture for distributed operations
"""

import time
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Supported event types"""
    DATA_RECEIVED = "data_received"
    PROCESS_START = "process_start"
    PROCESS_END = "process_end"
    ERROR = "error"
    ALERT = "alert"


dataclass class Event:
    """Represents a single event in the system"""
    event_type: EventType
    payload: Any
    timestamp: float
    
    def __str__(self):
        return f"Event({self.event_type.value}, {self.payload}, {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp))})"


class EventHandler:
    """Manages event handlers and processing"""    
    def __init__(self):
        self.handlers: Dict[EventType, List[Callable]] = {event_type: [] for event_type in EventType}
        self.event_log: List[Event] = []
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe a handler to an event type"""
        self.handlers[event_type].append(handler)
        print(f"✓ Subscribed handler to {event_type.value}")
    
    def emit(self, event: Event):
        """Emit an event and trigger all associated handlers"""
        self.event_log.append(event)
        print(f"→ Emitting: {event}")
        
        for handler in self.handlers[event.event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"✗ Error in handler: {e}")
    
    def get_event_log(self) -> List[Event]:
        """Retrieve the event log"""
        return self.event_log


class DataProcessor:
    """Simple data processor with event-driven architecture"""    
    def __init__(self, event_handler: EventHandler):
        self.event_handler = event_handler
        self.processed_count = 0
        
        # Register handlers
        self.event_handler.subscribe(EventType.DATA_RECEIVED, self.process_data)
    
    def process_data(self, event: Event):
        """Process incoming data"""
        data = event.payload
        print(f"  → Processing data: {data}")
        
        # Emit process start event
        start_event = Event(EventType.PROCESS_START, data, time.time())
        self.event_handler.emit(start_event)
        
        # Simulate processing
        time.sleep(0.1)
        
        # Emit process end event
        end_event = Event(EventType.PROCESS_END, f"Processed: {data}", time.time())
        self.event_handler.emit(end_event)
        
        self.processed_count += 1


class WebNova:
    """Main WebNova Real-Time Processing Engine"""    
    def __init__(self):
        self.event_handler = EventHandler()
        self.processor = DataProcessor(self.event_handler)
    
    def process_batch(self, data_list: List[Any]):
        """Process a batch of data"""
        print(f"\n{'='*60}")
        print(f"WebNova Real-Time Processing Engine")
        print(f"Processing {len(data_list)} items...")
        print(f"{'='*60}\n")
        
        for data in data_list:
            event = Event(EventType.DATA_RECEIVED, data, time.time())
            self.event_handler.emit(event)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            "total_events": len(self.event_handler.event_log),
            "items_processed": self.processor.processed_count,
            "event_types": {
                event_type.value: len([e for e in self.event_handler.event_log if e.event_type == event_type])
                for event_type in EventType
            }
        }


def main():
    """Example usage of WebNova"""
    # Initialize the engine
    engine = WebNova()
    
    # Custom handler example
    def alert_handler(event: Event):
        print(f"  🔔 Alert: {event.payload}")
    
    engine.event_handler.subscribe(EventType.PROCESS_END, alert_handler)
    
    # Process sample data
    sample_data = ["sensor_reading_1", "sensor_reading_2", "sensor_reading_3", "sensor_reading_4"]
    engine.process_batch(sample_data)
    
    # Display statistics
    print(f"\n{'='*60}")
    print("Processing Statistics:")
    print(f"{'='*60}")
    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()