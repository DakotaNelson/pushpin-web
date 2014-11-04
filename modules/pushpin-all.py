import module
import framework
# unique to module
import sys

class Module(module.Module):

    def __init__(self, params):
        module.Module.__init__(self, params)
        self.register_option('latitude', None, True, 'latitude of the epicenter')
        self.register_option('longitude', None, True, 'longitude of the epicenter')
        #self.register_option('address', None, False, 'address of the target location')
        self.register_option('radius', 1, True, 'radius in kilometers')
        self.register_option('map_filename', '%s/pushpin_map.html' % (self.workspace), True, 'path and filename for pushpin map report')
        self.register_option('media_filename', '%s/pushpin_media.html' % (self.workspace), True, 'path and filename for pushpin media report')
        self.info = {
                     'Name': 'Pushpin Run-All',
                     'Author': 'Dakota Nelson',
                     'Description': 'Runs all of the pushpin modules for which there are keys, and then generates a report.',
                     }

    def module_run(self):
        # get all pushpin modules
        pushpinModules = [x for x in self.loaded_modules if "locations-pushpins" in x]
        if self.modulename in pushpinModules: pushpinModules.remove(self.modulename) # infinite recursion = bad

        # add the specified location (if any) to the locations database
        lat = self.options['latitude']
        lon = self.options['longitude'] # I'm lazy
        self.add_locations(lat,lon)

        #points = self.query('SELECT DISTINCT latitude || \',\' || longitude FROM locations WHERE latitude IS NOT NULL AND longitude IS NOT NULL')
        self.output("Adding specified latitude/longitude to locations table.")

        # run each pushpin module
        for pushpinModule in pushpinModules:
            print('')
            self.heading("Starting " + pushpinModule, level=1)
            loadedName = self.loaded_modules[pushpinModule]
            toRun = sys.modules[loadedName].Module(('',pushpinModule))
            toRun.options['radius'] = self.options['radius']
            # run the module
            toRun.do_run(('',pushpinModule))

        print('')
        self.heading("Compiling Report", level=1)
        # load the report
        report = sys.modules['reporting_pushpin'].Module(('',''))
        # pass down options
        report.options.update(self.options)
        # and go
        report.do_run(('',''))
