"""
Functions to access Analogs Project Structure

Description
----
Replacement class for Analog_Tools.Analog_Structure


Structure can be broken down into levels

- Project
    - Prod
        - ProdChild

- ####_Template_Project
    - A_MANAGEMENT
    - B_DATA
    - C_PRE_PRODUCTION (a prefix for a duplicate of 3D & 2D)
        - D_3D_PRODUCTION
        - E_2D_PRODUCTION
    - D_3D_PRODUCTION
        - 01_MASTER_ASSETS
        - 02_SCULPTING
        - 03_SHOTS
        - 04_TRACKING
        - 05_SHADERS
        - 99_MAPS
        - 99_MISC
    - E_2D_PRODUCTION
        - 00_GLOBALELEMENTS
        - 01_MASTER_ASSETS
        - 03_SHOTS
    - F_POST_PRODUCTION
        - 01_EDIT
        - 02_FOOTAGE
        - 03_AUDIO
        - 04_AE_EXPORTS
        - 05_RESOLVE
    - G_DAILIES
    - H_DELIVERY
    - I_MAKINGOF

"""
import os
import logging
import pprint
import tomli
from deprecated import deprecated

class Structure:
    """
    removed any sensitive info
    """

    def __init__(self):
        self.read_config_file()

    def read_config_file(self):
        """Load toml file from $AN_STRUCTURE_CONFIG"""

        # ini config parsing
        config_file_path = os.getenv('AN_STRUCTURE_CONFIG').replace('\\', '/')

        if not config_file_path:
            logging.error('Envionment variable \"AN_STRUCTURE_CONFIG\" is missing')
            return False
        
        # print('{n} - loading toml config file: {v}'.format(n=__name__, v=config_file_path))

        # toml
        with open(config_file_path, mode='rb') as fp:
            self.config = tomli.load(fp)

        # # test configproject3
        # config_project3 = self.config.get('project3')

        # for child in config_project3.get('children'):
        #     print('{}'.format(child['dir']))
            
        #     if child.get('children'):
        #         for child2 in child.get('children'):
        #             print('\t{}'.format(child2['dir']))

        #         if child2.get('children'):
        #             for child3 in child2.get('children'):
        #                 print('\t\t{}'.format(child3['dir']))

    def get_shot_prefix(self):
        """Returns the string that prefixes a shot ie. 'Shot'_001"""
        return 'Shot'

    def get_3dasset_dirname(self):
        """Returns a string for the folder name where the 3dassets live ie. 01_MASTER_ASSETS"""
        return self.config.get('project').get('AssetsDir')

    def get_3dshots_dirname(self):
        """Returns a string for the folder name of the parent of all the shot folders i.e 03_SHOTS"""
        return self.config.get('project').get('ShotsDir')

    def get_projects_root(self):
        """replaces oProjectRoot"""

        if os.getenv('AN_PROJECTS'):
            return os.getenv('AN_PROJECTS')
        
        return os.getenv('ANALOG_PROJECTS')

    def get_pitches_root(self):
        """Still using ini"""
        return self.config.get('Analog', 'Pitches')

    def get_resouces_root(self):
        """replaces oResourcesRoot"""

        if os.getenv('AN_RESOURCES'):
            return os.getenv('AN_RESOURCES')
        
        return os.getenv('ANALOG_RESOURCES')        


    @deprecated(version='0.1.0', reason='GetPublishedRoot() - Publish no longer (2017) copying to a seperate share so this shouldnt be called')
    def get_published_root(self):
        return None

    def get_deadline_repository_path(self):
        """This used to be in the ini, but use a env var now"""
    
        if os.getenv('AN_DEADLINE_REPOSITORY'):
            return os.getenv('AN_DEADLINE_REPOSITORY')
        
        return os.getenv('ANALOG_DEADLINE_REPOSITORY')

    @deprecated(version='0.1.0', reason="Dailies has been retired.")
    def get_dailies_url(self):
        return None

    def get_prod_management(self):
        return 'A_MANAGEMENT'

    def get_prod_data(self):
        return 'B_DATA'

    def get_prod_pre(self):
        return self.config.get('project').get('PreProdDir')

    def get_prod_3d(self):
        return self.config.get('project').get('3DProdDir')

    def get_prod_2d(self):
        return self.config.get('project').get('2DProdDir')

    def get_prod_post(self):
        return self.config.get('project').get('PostProdDir')

    def get_prod_dailies(self):
        return self.config.get('project').get('DailiesDir')

    def get_prod_delivery(self):
        return 'H_DELIVERY'

    def get_prods(self):
        """
        Returns a dict of all the production dir names
        """

        prod_dirs = {
            'management' : self.get_prod_management(),
            'data' : self.get_prod_data(),
            'pre' : self.get_prod_pre(),
            '3d' : self.get_prod_3d(),
            '2d' : self.get_prod_2d(),
            'post' : self.get_prod_post(),
            'dailies' : self.get_prod_dailies(),
            'delivery' :self.get_prod_delivery(),
        }

        return prod_dirs


    def get_shot_children_2d(self, project_index=9999):
        """
        Returns a dict providing names of folders

        Used to require ProjectIndex, now assume the latest structure version by using 9999
         - 2019 now return a dict
        """

        shot_children_2d = {
            'scripts' : self.config.get('project').get('2DScriptsDir'),
            'renders' : self.config.get('project').get('2DRendersDir'),
            'elements' : self.config.get('project').get('2DElementsDir'),
            'outputs' : self.config.get('project').get('2DOutputsDir'),
            'previews' : self.config.get('project').get('2DPreviewsDir'),
            'footage' :  self.config.get('project').get('2DFootageDir')
        }

        return shot_children_2d

    def get_shot_children_3d(self, project_index=9999):
        """
        Returns a dict providing names of folders

        This used to not even be in the ini file so I added them there too
        """

        shot_children_3d = {
            'scenes' : self.config.get('project').get('3DScenesDir'),
            'maps' : self.config.get('project').get('3DMapsDir'),
            'caches' : self.config.get('project').get('3DCachesDir'),
            'exports' : self.config.get('project').get('3DExportDir'),
        }

        return shot_children_3d

    def get_prod_children_3d(self, project_index=9999):
        """
        Returns a dict providing names of folders
        """

        prod_children_3d = {
            'assets' : self.get_3dasset_dirname(),
            # 'sculpting' : self.config.get('project').get('3DMapsDir'),
            'shots' : self.get_3dshots_dirname()
            # 'tracking' : self.config.get('project').get('3DExportDir'),
            # 'shaders' : self.config.get('project').get('3DExportDir'),
            # 'maps' : self.config.get('project').get('3DExportDir'),
            # 'misc' : self.config.get('project').get('3DExportDir'),
        }

        return prod_children_3d
