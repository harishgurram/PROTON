# BSD 3-Clause License
#
# Copyright (c) 2018, Pruthvi Kumar All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from jinja2 import Environment, FileSystemLoader
from nucleus.db.cache_manager import CacheManager

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class MetaGen(CacheManager):

    def __init__(self):
        super(MetaGen, self).__init__()
        self.metagen_logger = self.get_logger(log_file_name='meta_gen_logs',
                                              log_file_path='{}/trace/meta_gen_logs.log'.format(self.ROOT_DIR))
        self.__models_root = '{}/mic/models'.format(self.ROOT_DIR)
        self.__controllers_root = '{}/mic/controllers'.format(self.ROOT_DIR)
        self.__main_executable = '{}/main.py'.format(self.ROOT_DIR)
        self.__jinja_env = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__models_template = self.__jinja_env.get_template('model_template.py')
        self.__controllers_template = self.__jinja_env.get_template('controller_template.py')

        self.bootstrap_sqlite = self.__sqlite_meta_generator
        self.new_mic = self.__meta_generator

    def __sqlite_meta_generator(self):
        """
        Generate core tables in SQLite for PROTON.
        :return: boolean
        """
        from configuration import ProtonConfig
        from nucleus.db.connection_manager import ConnectionManager
        from sqlalchemy import MetaData, Table, Column, Integer, DateTime, String, ForeignKey

        try:
            if ProtonConfig.TARGET_DB == 'sqlite':
                engine = ConnectionManager.alchemy_engine()[ProtonConfig.TARGET_DB]
                metadata = MetaData(bind=engine)
                self.metagen_logger.info('Bootstrapping key tables for PROTONs SQLITE')
                # Create User & Login registry if not exists.
                if not engine.dialect.has_table(engine, 'PROTON_user_registry'):
                    # Create default PROTON user registry.
                    Table('PROTON_user_registry', metadata,
                          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                          Column('first_name', String, nullable=False),
                          Column('last_name', String, nullable=False),
                          Column('email', String, nullable=False),
                          Column('creation_date_time', DateTime, nullable=False))
                    metadata.create_all()
                    self.metagen_logger.info('PROTON_user_registry created.')

                if not engine.dialect.has_table(engine, 'PROTON_login_registry'):
                    # Create default PROTON user registry.
                    Table('PROTON_login_registry', metadata,
                          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                          Column('user_registry_id', Integer, ForeignKey('PROTON_user_registry.id', onupdate="CASCADE",
                                                                         ondelete="CASCADE"), nullable=False),
                          Column('user_name', String, nullable=False),
                          Column('password', String, nullable=False),
                          Column('last_login_date_time', DateTime, nullable=True))
                    metadata.create_all()
                    self.metagen_logger.info('PROTON_login_registry created.')

                # Create default table if not exists.
                if not engine.dialect.has_table(engine, 'PROTON_default'):
                    # Create a table with the appropriate columns
                    Table('PROTON_default', metadata,
                          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                          Column('Creation_Date_Time', DateTime),
                          Column('Deletion_Date_Time', DateTime, nullable=True),
                          Column('Target_MIC_Stack', String),
                          Column('Target_Database', String),
                          Column('Target_Table', String))
                    metadata.create_all()
                    self.metagen_logger.info('PROTON_default created.')
                self.metagen_logger.info('SQLite is bootstrapped and ready to serve PROTON.')
                return True
            return False
        except Exception as e:
            self.metagen_logger.exception(
                '[Metagen]: Could not successfully create PROTON default db & PROTON default table. '
                'Stack trace to follow.')
            self.metagen_logger.exception(str(e))
            return False

    def __meta_generator(self, mic_name):
        """
        Generate structure for everything from models, & controllers.
        :param mic_name:
        :return:
        """

        # Generate default PROTON db in desired db_flavour if it doesnt already exist.
        from configuration import ProtonConfig
        from nucleus.db.connection_manager import ConnectionManager
        from sqlalchemy import MetaData, Table
        from datetime import datetime

        try:
            with open('{}/proton_vars/target_table_for_{}.txt'.format(self.ROOT_DIR, mic_name)) as f:
                target_table_for_mic = f.read().replace('\n', '')

            engine = ConnectionManager.alchemy_engine()[ProtonConfig.TARGET_DB]
            metadata = MetaData(bind=engine)
            if ProtonConfig.TARGET_DB == 'sqlite':

                if self.__sqlite_meta_generator():

                    # Add row to default DB
                    proton_default = Table('PROTON_default', metadata, autoload=True)
                    ins = proton_default.insert()
                    ins.execute({"Creation_Date_Time": datetime.utcnow(),
                                 "Target_MIC_Stack": mic_name,
                                 "Target_Database": ProtonConfig.TARGET_DB,
                                 "Target_Table": target_table_for_mic})
                else:
                    raise Exception('SQLite is missing key tables required for PROTON to function.')
        except Exception as e:
            self.metagen_logger.exception(
                '[Metagen]: Could not successfully create PROTON default db & PROTON default table OR'
                ' insert new row in PROTON default db for MIC stack - {}. Stack trace to '
                'follow.'.format(mic_name))
            self.metagen_logger.exception(str(e))

        # Create MIC Stack
        new_model = self.__models_root + '/{}'.format(mic_name)
        try:
            if not os.path.exists(new_model):
                os.makedirs(new_model)
                open(new_model + '/__init__.py', 'w+').close()
                # open(new_model + '/model_{}.py'.format(mic_name), 'w+').close()
                with open(new_model + '/model_{}.py'.format(mic_name), 'w+') as mf:
                    mf.write(self.__models_template.render(modelName=mic_name))
                # Generate Controllers for newly created model.
                with open(self.__controllers_root + '/controller_{}.py'.format(mic_name), 'w+') as cf:
                    cf.write(self.__controllers_template.render(modelName=mic_name, controllerName=mic_name))

                return ('Meta Structure of models & controllers for {} successfully created!'.format(mic_name))
            else:
                raise Exception('[MetaGen]: File/Folder named {} already exists in path {}. MetaGen will require '
                                'unique names for it to generate MIC structure.'.format(mic_name, new_model))

        except Exception as e:
            self.metagen_logger.exception('[MetaGen]: Exception during instantiating MIC stack for {}. '
                                          'Details: {}'.format(mic_name, str(e)))
